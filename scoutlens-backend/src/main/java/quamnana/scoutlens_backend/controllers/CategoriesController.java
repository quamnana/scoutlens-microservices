package quamnana.scoutlens_backend.controllers;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.AllArgsConstructor;
import quamnana.scoutlens_backend.services.CategoryService;

@RestController
@AllArgsConstructor
@RequestMapping("/categories")
public class CategoriesController {
    private CategoryService categoryService;

    @GetMapping("/{field}")
    public ResponseEntity<List<String>> getTeamsByLeague(@PathVariable String field,
            @RequestParam(required = false) String league) {
        List<String> teams = categoryService.getCategories(field, league);
        return new ResponseEntity<>(teams, HttpStatus.OK);
    }
}
