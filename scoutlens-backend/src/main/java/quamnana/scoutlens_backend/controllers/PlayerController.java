package quamnana.scoutlens_backend.controllers;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.AllArgsConstructor;
import quamnana.scoutlens_backend.dtos.PlayerBasicInfo;
import quamnana.scoutlens_backend.dtos.PlayerComparison;
import quamnana.scoutlens_backend.dtos.overview.OverviewData;
import quamnana.scoutlens_backend.entities.Player;
import quamnana.scoutlens_backend.services.PlayerService;

import java.util.List;
import java.util.Map;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@RestController
@AllArgsConstructor
@RequestMapping("/players")
public class PlayerController {
    private PlayerService playerService;

    @GetMapping
    public ResponseEntity<Page<PlayerBasicInfo>> getPlayersWithFilters(
            @RequestParam Map<String, Object> filterParams,
            @PageableDefault(size = 10, sort = "position") Pageable pageable) {
        Page<PlayerBasicInfo> players = playerService.getPlayers(filterParams, pageable);
        return new ResponseEntity<>(players, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Player> getPlayer(@PathVariable String id) {
        Player player = playerService.getPlayer(id);
        return new ResponseEntity<>(player, HttpStatus.OK);
    }

    @GetMapping("/compare")
    public ResponseEntity<PlayerComparison> comparePlayers(@RequestParam String player1Id,
            @RequestParam String player2Id) {
        PlayerComparison comparisonResult = playerService.comparePlayers(player1Id, player2Id);

        return new ResponseEntity<>(comparisonResult, HttpStatus.OK);
    }

    @GetMapping("/overview")
    public ResponseEntity<OverviewData> getOverview() {
        OverviewData overiew = playerService.getOverview();

        return new ResponseEntity<>(overiew, HttpStatus.OK);
    }
}
