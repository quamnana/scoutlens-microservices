package quamnana.scoutlens_backend.dtos;

import lombok.Getter;

@Getter
public class PlayerBasicInfo {
    private String id;
    private String fullName;
    private String nation;
    private String position;
    private String team;
    private String league;
    private int age;
}