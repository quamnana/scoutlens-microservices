package quamnana.scoutlens_backend.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.support.PageableExecutionUtils;
import org.springframework.stereotype.Service;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import lombok.AllArgsConstructor;
import quamnana.scoutlens_backend.dtos.PlayerBasicInfo;
import quamnana.scoutlens_backend.dtos.PlayerComparison;
import quamnana.scoutlens_backend.dtos.overview.OverviewData;
import quamnana.scoutlens_backend.entities.Player;
import quamnana.scoutlens_backend.repositories.PlayerRepository;
import quamnana.scoutlens_backend.utils.OverviewUtil;

@Service
@AllArgsConstructor
public class PlayerServiceImpl implements PlayerService {
    private PlayerRepository playerRepository;
    private final MongoTemplate mongoTemplate;
    private OverviewUtil overviewUtil;

    @Override
    public Page<PlayerBasicInfo> getPlayers(Map<String, Object> filterParams, Pageable pageable) {
        Query query = createQuery(filterParams);

        // Project only required fields
        query.fields()
                .include("_id")
                .include("fullName")
                .include("team")
                .include("position")
                .include("nation")
                .include("league")
                .include("age");

        // Get total count before applying pagination
        long total = mongoTemplate.count(query, PlayerBasicInfo.class, "players");

        // Apply pagination and sorting
        query.with(pageable);

        // Execute query with pagination
        List<PlayerBasicInfo> players = mongoTemplate.find(query, PlayerBasicInfo.class, "players");

        // Create pageable response
        return PageableExecutionUtils.getPage(
                players,
                pageable,
                () -> total);
    }

    private Query createQuery(Map<String, Object> filterParams) {
        Query query = new Query();

        if (filterParams != null && !filterParams.isEmpty()) {
            filterParams.forEach((key, value) -> {
                if (value != null) {
                    // Handle different types of filters
                    if (value instanceof String) {
                        // For string values, you might want to use case-insensitive regex
                        query.addCriteria(Criteria.where(key)
                                .regex((String) value, "i"));
                    } else {
                        query.addCriteria(Criteria.where(key).is(value));
                    }
                }
            });
        }

        return query;
    }

    @Override
    public Player getPlayer(String id) {
        return playerRepository.findById(id).get();
    }

    @Override
    public PlayerComparison comparePlayers(String player1Id, String player2Id) {
        Player player1 = playerRepository.findById(player1Id).get();
        Player player2 = playerRepository.findById(player2Id).get();
        return new PlayerComparison(player1, player2);
    }

    public OverviewData getOverview() {
        return new OverviewData(
                overviewUtil.getCountriesData(),
                overviewUtil.getLeaguesData(),
                overviewUtil.getTopGoalScorers(),
                overviewUtil.getTopAssists(),
                overviewUtil.getTopPassers(),
                overviewUtil.getTopTacklers());
    }

    @Override
    public Page<Player> findPlayersWithFilters(
            Map<String, String> filters,
            Pageable pageable) {

        try {
            // Create the query
            Query query = new Query();

            // Apply filters if they exist
            if (filters != null && !filters.isEmpty()) {
                List<Criteria> criteriaList = new ArrayList<>();

                filters.forEach((key, value) -> {
                    if (value != null && !value.trim().isEmpty()) {
                        // Handle different fields differently if needed
                        switch (key) {
                            case "age":
                                try {
                                    int age = Integer.parseInt(value);
                                    criteriaList.add(Criteria.where(key).is(age));
                                } catch (NumberFormatException e) {
                                }
                                break;

                            case "fullName":
                            case "team":
                            case "position":
                            case "nation":
                            case "league":
                                // Case-insensitive regex search for string fields
                                criteriaList.add(Criteria.where(key)
                                        .regex(value, "i"));
                                break;

                            default:
                                break;
                        }
                    }
                });

                // Combine all criteria with AND operation
                if (!criteriaList.isEmpty()) {
                    query.addCriteria(new Criteria().andOperator(
                            criteriaList.toArray(new Criteria[0])));
                }
            }

            // Get total count for pagination
            long total = mongoTemplate.count(query, Player.class);

            // Apply pagination
            query.with(pageable);

            // Execute query
            List<Player> players = mongoTemplate.find(query, Player.class);

            // Create pageable result
            return PageableExecutionUtils.getPage(
                    players,
                    pageable,
                    () -> total);

        } catch (Exception e) {
            throw new RuntimeException("Error retrieving players", e);
        }
    }

}
