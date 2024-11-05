package quamnana.scoutlens_backend.dtos.overview;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class OverviewData {
    private List<CountryData> countriesData;
    private List<LeagueData> leaguesData;
    private List<TopPlayerStat> topGoalScorers;
    private List<TopPlayerStat> topAssists;
    private List<TopPlayerStat> topPassers;
    private List<TopPlayerStat> topTacklers;

}
