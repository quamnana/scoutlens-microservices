package quamnana.scoutlens_backend.services;

import java.util.List;

import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.Aggregation;
import org.springframework.data.mongodb.core.aggregation.AggregationResults;
import org.springframework.data.mongodb.core.aggregation.GroupOperation;
import org.springframework.data.mongodb.core.aggregation.ProjectionOperation;
import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import quamnana.scoutlens_backend.dtos.overview.CountryData;
import quamnana.scoutlens_backend.dtos.overview.LeagueData;
import quamnana.scoutlens_backend.dtos.overview.TopPlayerStat;

@Service
@AllArgsConstructor
public class OverviewService {
    private MongoTemplate mongoTemplate;

    public List<CountryData> getCountriesData() {
        GroupOperation groupByNation = Aggregation.group("nation").first("nation").as("nation").count().as("players");
        Aggregation aggregation = Aggregation.newAggregation(groupByNation);

        AggregationResults<CountryData> result = mongoTemplate.aggregate(aggregation, "players", CountryData.class);
        return result.getMappedResults();
    }

    public List<LeagueData> getLeaguesData() {
        // Step 1: Group by "league" to count players and unique teams in each league
        GroupOperation groupByLeague = Aggregation.group("league")
                .first("league").as("league")
                .count().as("players")
                .addToSet("team").as("uniqueTeams");

        // Step 2: Project the fields to match LeagueData DTO, counting unique teams
        ProjectionOperation projectFields = Aggregation.project("league", "players")
                .andExpression("size(uniqueTeams)").as("teams");

        Aggregation aggregation = Aggregation.newAggregation(
                groupByLeague,
                projectFields);

        AggregationResults<LeagueData> result = mongoTemplate.aggregate(aggregation, "players", LeagueData.class);
        return result.getMappedResults();
    }

    private List<TopPlayerStat> getTopStat(String stat, int topN) {
        Aggregation aggregation = Aggregation.newAggregation(
                Aggregation.sort(Sort.by(Sort.Direction.DESC, stat)),
                Aggregation.limit(topN),
                Aggregation.project("team", stat, "fullName")
                        .and(stat).as("stats")
                        .and("fullName").as("name"));

        AggregationResults<TopPlayerStat> result = mongoTemplate.aggregate(aggregation, "players", TopPlayerStat.class);
        return result.getMappedResults();
    }

    public List<TopPlayerStat> getTopGoalScorers() {
        return getTopStat("goalsScored", 3);
    }

    public List<TopPlayerStat> getTopAssists() {
        return getTopStat("assists", 3);
    }

    public List<TopPlayerStat> getTopPassers() {
        return getTopStat("totalPassesCompleted", 3);
    }

    public List<TopPlayerStat> getTopTacklers() {
        return getTopStat("tackles", 3);

    }

}
