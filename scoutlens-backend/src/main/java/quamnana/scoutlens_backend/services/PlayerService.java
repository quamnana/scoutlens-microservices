package quamnana.scoutlens_backend.services;

import java.util.Map;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import quamnana.scoutlens_backend.dtos.PlayerBasicInfo;
import quamnana.scoutlens_backend.dtos.PlayerComparison;
import quamnana.scoutlens_backend.dtos.overview.OverviewData;
import quamnana.scoutlens_backend.entities.Player;

public interface PlayerService {
    Page<PlayerBasicInfo> getPlayers(Map<String, Object> filterParams, Pageable pageable);

    Player getPlayer(String id);

    PlayerComparison comparePlayers(String player1Id, String player2Id);

    OverviewData getOverview();

    Page<Player> findPlayersWithFilters(
            Map<String, String> filters, Pageable pageable);
}