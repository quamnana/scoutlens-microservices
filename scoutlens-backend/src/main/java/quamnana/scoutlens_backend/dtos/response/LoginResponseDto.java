package quamnana.scoutlens_backend.dtos.response;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class LoginResponseDto {
    private String id;
    private String firstName;
    private String lastName;
    private String username;
    private String email;
    private String team;
    private String token;
}
