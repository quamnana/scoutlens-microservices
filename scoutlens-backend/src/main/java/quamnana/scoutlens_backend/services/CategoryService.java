package quamnana.scoutlens_backend.services;

import java.util.List;

public interface CategoryService {
    List<String> getCategories(String field, String league);
}
