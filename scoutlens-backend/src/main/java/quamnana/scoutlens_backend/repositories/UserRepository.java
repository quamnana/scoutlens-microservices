package quamnana.scoutlens_backend.repositories;

import quamnana.scoutlens_backend.entities.User;

import java.util.Optional;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface UserRepository extends MongoRepository<User, String> {
    Optional<User> findByUsername(String username);

}
