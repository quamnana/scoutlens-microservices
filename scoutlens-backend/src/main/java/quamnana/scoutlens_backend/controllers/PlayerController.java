package quamnana.scoutlens_backend.controllers;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.AllArgsConstructor;
import quamnana.scoutlens_backend.dtos.PlayerBasicInfo;
import quamnana.scoutlens_backend.dtos.PlayerComparison;
import quamnana.scoutlens_backend.entities.Player;
import quamnana.scoutlens_backend.services.PlayerService;

import java.util.List;
import java.util.Map;

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
    public ResponseEntity<List<PlayerBasicInfo>> getPlayersWithFilters(
            @RequestParam Map<String, Object> filterParams) {
        List<PlayerBasicInfo> players = playerService.getPlayers(filterParams);
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

}
