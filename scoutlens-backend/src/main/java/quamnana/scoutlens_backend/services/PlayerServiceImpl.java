package quamnana.scoutlens_backend.services;

import java.util.List;

import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import quamnana.scoutlens_backend.entities.Player;
import quamnana.scoutlens_backend.repositories.PlayerRepository;

@Service
@AllArgsConstructor
public class PlayerServiceImpl implements PlayerService {
    private PlayerRepository playerRepository;

    @Override
    public List<Player> getPlayers() {
        return playerRepository.findAll();
    }
}
