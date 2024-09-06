// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract Tournament {
    struct Match {
        string tournament_id;
        string player_id_1;
        string player_id_2;
        string player_id_3;
        string player_id_4;
        string score_match_1_2;
        string score_match_3_4;
    }

    Match[] public matches;

    function saveMatch(
        string memory tournament_id,
        string memory player_id_1,
        string memory player_id_2,
        string memory player_id_3,
        string memory player_id_4,
        string memory score_match_1_2,
        string memory score_match_3_4
    ) public {
        matches.push(Match(
            tournament_id,
            player_id_1,
            player_id_2,
            player_id_3,
            player_id_4,
            score_match_1_2,
            score_match_3_4
        ));
    }

    function getMatches() public view returns (Match[] memory) {
        return matches;
    }
}