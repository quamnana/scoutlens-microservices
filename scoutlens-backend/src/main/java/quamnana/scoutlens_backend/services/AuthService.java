package quamnana.scoutlens_backend.services;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import quamnana.scoutlens_backend.dtos.response.SignUpResponseDto;
import quamnana.scoutlens_backend.dtos.response.LoginResponseDto;
import quamnana.scoutlens_backend.entities.User;
import quamnana.scoutlens_backend.repositories.UserRepository;
import quamnana.scoutlens_backend.exceptions.UsernameAlreadyExistsException;
import quamnana.scoutlens_backend.exceptions.InvalidCredentialsException;
import quamnana.scoutlens_backend.exceptions.TokenGenerationException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.JwtException;
import lombok.AllArgsConstructor;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.Map;

@Service
@AllArgsConstructor
public class AuthService {
        private static final Logger logger = LoggerFactory.getLogger(AuthService.class);
        private static final long TOKEN_VALIDITY = 1000 * 60 * 60 * 10; // 10 hours

        private final UserRepository userRepository;
        private final BCryptPasswordEncoder passwordEncoder;
        private final SecretKey secretKey;

        @Transactional
        public SignUpResponseDto signup(User user) {
                logger.debug("Attempting to sign up user with username: {}", user.getUsername());

                // Validate user input
                validateUserInput(user);

                // Check if the username already exists
                if (userRepository.findByUsername(user.getUsername()).isPresent()) {
                        logger.warn("Signup failed: Username already exists: {}", user.getUsername());
                        throw new UsernameAlreadyExistsException(
                                        String.format("Username '%s' is already taken", user.getUsername()));
                }

                try {
                        // Encode password and save user
                        user.setPassword(passwordEncoder.encode(user.getPassword()));
                        User savedUser = userRepository.save(user);
                        logger.info("Successfully created new user with username: {}", user.getUsername());

                        return new SignUpResponseDto(
                                        savedUser.getId(),
                                        savedUser.getFirstName(),
                                        savedUser.getLastName(),
                                        savedUser.getUsername(),
                                        savedUser.getEmail(),
                                        savedUser.getTeam());
                } catch (Exception e) {
                        logger.error("Error during user registration", e);
                        throw new RuntimeException("Failed to register user", e);
                }
        }

        @Transactional(readOnly = true)
        public LoginResponseDto login(String username, String password) {
                logger.debug("Attempting login for user: {}", username);

                // Validate input
                if (username == null || username.trim().isEmpty() || password == null || password.trim().isEmpty()) {
                        throw new InvalidCredentialsException("Username and password are required");
                }

                try {
                        // Find user and verify credentials
                        User user = userRepository.findByUsername(username)
                                        .orElseThrow(() -> {
                                                logger.warn("Login failed: User not found: {}", username);
                                                return new InvalidCredentialsException("Invalid username or password");
                                        });

                        if (!passwordEncoder.matches(password, user.getPassword())) {
                                logger.warn("Login failed: Invalid password for user: {}", username);
                                throw new InvalidCredentialsException("Invalid username or password");
                        }

                        // Generate JWT token
                        String token = generateToken(user);
                        logger.info("Successfully logged in user: {}", username);

                        return new LoginResponseDto(
                                        user.getId(),
                                        user.getFirstName(),
                                        user.getLastName(),
                                        user.getUsername(),
                                        user.getEmail(),
                                        user.getTeam(),
                                        token);
                } catch (InvalidCredentialsException e) {
                        throw e;
                } catch (Exception e) {
                        logger.error("Error during login process", e);
                        throw new RuntimeException("Login process failed", e);
                }
        }

        private String generateToken(User user) {
                try {
                        return Jwts.builder()
                                        .setClaims(Map.of(
                                                        "username", user.getUsername(),
                                                        "email", user.getEmail()))
                                        .setSubject(user.getUsername())
                                        .setIssuedAt(new Date())
                                        .setExpiration(new Date(System.currentTimeMillis() + TOKEN_VALIDITY))
                                        .signWith(secretKey)
                                        .compact();
                } catch (JwtException e) {
                        logger.error("Failed to generate JWT token", e);
                        throw new TokenGenerationException("Failed to generate authentication token", e);
                }
        }

        private void validateUserInput(User user) {
                if (user == null) {
                        throw new IllegalArgumentException("User cannot be null");
                }
                if (user.getUsername() == null || user.getUsername().trim().isEmpty()) {
                        throw new IllegalArgumentException("Username is required");
                }
                if (user.getPassword() == null || user.getPassword().trim().isEmpty()) {
                        throw new IllegalArgumentException("Password is required");
                }
                if (user.getEmail() == null || user.getEmail().trim().isEmpty()) {
                        throw new IllegalArgumentException("Email is required");
                }
                // Add more validation as needed
        }
}