package quamnana.scoutlens_backend.controllers;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.AllArgsConstructor;
import quamnana.scoutlens_backend.dtos.PlayerComparison;
import quamnana.scoutlens_backend.dtos.overview.OverviewData;
import quamnana.scoutlens_backend.entities.Player;
import quamnana.scoutlens_backend.services.PlayerService;

import java.util.HashMap;
import java.util.Map;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@RestController
@AllArgsConstructor
@RequestMapping("/players")
public class PlayerController {
    private PlayerService playerService;

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

    @GetMapping
    public ResponseEntity<Map<String, Object>> getPlayers(
            @RequestParam(required = false) Map<String, String> filters,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "rank") String sortField,
            @RequestParam(defaultValue = "asc") String sortDir) {

        try {

            // Create Sort object
            Sort sort = Sort.by(
                    sortDir.equalsIgnoreCase("desc") ? Sort.Direction.DESC : Sort.Direction.ASC,
                    sortField);

            // Create Pageable object
            Pageable pageable = PageRequest.of(page, size, sort);

            // Get paginated and filtered result
            Page<Player> pageResult = playerService.findPlayersWithFilters(
                    filters,
                    pageable);

            // Create response
            Map<String, Object> response = new HashMap<>();
            response.put("players", pageResult.getContent());
            response.put("currentPage", pageResult.getNumber());
            response.put("totalItems", pageResult.getTotalElements());
            response.put("totalPages", pageResult.getTotalPages());
            response.put("size", pageResult.getSize());
            response.put("hasNext", pageResult.hasNext());
            response.put("hasPrevious", pageResult.hasPrevious());

            return new ResponseEntity<>(response, HttpStatus.OK);

        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "Error retrieving players");
            errorResponse.put("message", e.getMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

}
