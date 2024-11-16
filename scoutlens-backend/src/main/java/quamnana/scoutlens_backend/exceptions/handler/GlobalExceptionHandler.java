package quamnana.scoutlens_backend.exceptions.handler;

import org.springframework.http.HttpStatus; // Missing import
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import quamnana.scoutlens_backend.exceptions.InvalidCredentialsException;
import quamnana.scoutlens_backend.exceptions.TokenGenerationException;
import quamnana.scoutlens_backend.exceptions.UsernameAlreadyExistsException;
import quamnana.scoutlens_backend.dtos.response.ErrorResponse; // Use custom ErrorResponse

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UsernameAlreadyExistsException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ErrorResponse handleUsernameAlreadyExists(UsernameAlreadyExistsException ex) {
        return new ErrorResponse(ex.getMessage());
    }

    @ExceptionHandler(InvalidCredentialsException.class)
    @ResponseStatus(HttpStatus.UNAUTHORIZED)
    public ErrorResponse handleInvalidCredentials(InvalidCredentialsException ex) {
        return new ErrorResponse(ex.getMessage());
    }

    @ExceptionHandler(TokenGenerationException.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleTokenGeneration(TokenGenerationException ex) {
        return new ErrorResponse("Authentication failed");
    }
}
