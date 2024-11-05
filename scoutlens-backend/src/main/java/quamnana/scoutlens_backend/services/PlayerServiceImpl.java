package quamnana.scoutlens_backend.services;

import java.util.List;
import java.util.Map;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;

import lombok.AllArgsConstructor;
import quamnana.scoutlens_backend.dtos.PlayerBasicInfo;
import quamnana.scoutlens_backend.dtos.PlayerComparison;
import quamnana.scoutlens_backend.entities.Player;
import quamnana.scoutlens_backend.repositories.PlayerRepository;

@Service
@AllArgsConstructor
public class PlayerServiceImpl implements PlayerService {
    private PlayerRepository playerRepository;
    private final MongoTemplate mongoTemplate;

    @Override
    public Page<PlayerBasicInfo> getPlayers(Map<String, Object> filterParams, Pageable pageable) {
        Query query = new Query();

        for (Map.Entry<String, Object> entry : filterParams.entrySet()) {
            if (entry.getValue() != null) {
                query.addCriteria(Criteria.where(entry.getKey()).is(entry.getValue()));
            }
        }

        query.fields().include("_id", "fullName", "team", "position", "nation", "league", "age");

        // Enable pagination and sorting
        long count = mongoTemplate.count(query, PlayerBasicInfo.class, "players");
        List<PlayerBasicInfo> players = mongoTemplate.find(query.with(pageable), PlayerBasicInfo.class, "players");

        return new PageImpl<>(players, pageable, count);

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

}
