package quamnana.scoutlens_backend.services;

import java.util.List;
import java.util.Map;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

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
    public List<PlayerBasicInfo> getPlayers(Map<String, Object> filterParams) {
        Query query = new Query();

        for (Map.Entry<String, Object> entry : filterParams.entrySet()) {
            if (entry.getValue() != null) {
                query.addCriteria(Criteria.where(entry.getKey()).is(entry.getValue()));
            }
        }

        query.fields().include("_id", "fullName", "team", "position", "nation", "league", "age");

        return mongoTemplate.find(query, PlayerBasicInfo.class, "players");

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
