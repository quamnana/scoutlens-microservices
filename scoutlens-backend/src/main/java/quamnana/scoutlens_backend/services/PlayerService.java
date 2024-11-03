package quamnana.scoutlens_backend.services;

import java.util.List;
import java.util.Map;

import quamnana.scoutlens_backend.dtos.PlayerBasicInfo;
import quamnana.scoutlens_backend.dtos.PlayerComparison;
import quamnana.scoutlens_backend.entities.Player;

public interface PlayerService {
    List<PlayerBasicInfo> getPlayers(Map<String, Object> filterParams);

    Player getPlayer(String id);

    PlayerComparison comparePlayers(String player1Id, String player2Id);

}