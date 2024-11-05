package quamnana.scoutlens_backend.services;

import java.util.List;
import java.util.stream.Collectors;

import org.bson.Document;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.Aggregation;
import org.springframework.data.mongodb.core.aggregation.AggregationResults;
import org.springframework.data.mongodb.core.aggregation.GroupOperation;
import org.springframework.data.mongodb.core.aggregation.MatchOperation;
import org.springframework.data.mongodb.core.aggregation.ProjectionOperation;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class CategoryServiceImpl implements CategoryService {

    private final MongoTemplate mongoTemplate;

    @Override
    public List<String> getCategories(String field, String league) {

        if (field.equals("teams")) {
            List<String> teams = getTeamsByLeague(league);
            return teams;
        } else {
            Query query = new Query();
            return mongoTemplate.findDistinct(query, field, "players", String.class);
        }

    }

    private List<String> getTeamsByLeague(String league) {
        // Step 1: Match the specified league
        MatchOperation matchLeague = Aggregation.match(
                org.springframework.data.mongodb.core.query.Criteria.where("league").is(league));

        // Step 2: Group by team name to get unique team names
        GroupOperation groupByTeam = Aggregation.group("team");

        // Step 3: Project team name directly to remove the "_id" wrapper
        ProjectionOperation projectTeamName = Aggregation.project().and("_id").as("team");

        // Create aggregation pipeline
        Aggregation aggregation = Aggregation.newAggregation(matchLeague,
                groupByTeam, projectTeamName);

        // Execute aggregation and retrieve results as a list of maps, then extract
        // names
        AggregationResults<Document> result = mongoTemplate.aggregate(aggregation,
                "players", Document.class);

        return result.getMappedResults().stream()
                .map(doc -> doc.getString("team"))
                .collect(Collectors.toList());
    }
}
