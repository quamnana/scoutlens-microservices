package quamnana.scoutlens_backend.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import quamnana.scoutlens_backend.entities.Player;

@Repository
public interface PlayerRepository extends MongoRepository<Player, String> {

}