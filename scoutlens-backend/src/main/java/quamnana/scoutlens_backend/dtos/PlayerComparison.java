package quamnana.scoutlens_backend.dtos;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import quamnana.scoutlens_backend.entities.Player;

@Getter
@Setter
@AllArgsConstructor
public class PlayerComparison {
    private Player player1;
    private Player player2;
}
