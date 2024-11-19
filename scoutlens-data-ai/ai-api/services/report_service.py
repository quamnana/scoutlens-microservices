import openai


class ReportService:

    openai.api_key = ""

    def generate_prompt(self, player_data):
        return (
            f"Generate a detailed football scouting report for the following player data:\n\n"
            f"Player: {player_data.get('fullName')} ({player_data.get('age')} years old)\n"
            f"Position: {player_data.get('position')}\n"
            f"Team: {player_data.get('team')} ({player_data.get('league')})\n\n"
            f"Key Performance Metrics:\n"
            f"- {player_data.get('matchesPlayed')} matches played ({player_data.get('matchesStarted')} starts)\n"
            f"- {player_data.get('minutesPlayed')} minutes played\n"
            f"- {player_data.get('goalsScored')} goals, {player_data.get('assists')} assists\n"
            f"- Shot conversion rate: {player_data.get('shotConversionRate')}%\n"
            f"- Pass completion: {player_data.get('passCompletionPercentage')}%\n"
            f"- Take-on success rate: {player_data.get('takeOnSuccessPercentage')}%\n\n"
            f"Detailed Statistics:\n"
            f"Attacking: Goals per shot ({player_data.get('goalsPerShot')}), Shots on target % ({player_data.get('shotsOnTargetPercentage')})\n"
            f"Passing: Short {player_data.get('shortPassCompletionPercentage')}%, Medium {player_data.get('mediumPassCompletionPercentage')}%, Long {player_data.get('longPassCompletionPercentage')}%\n"
            f"Creation: {player_data.get('shotCreatingActions')} shot-creating actions, {player_data.get('goalCreatingActions')} goal-creating actions\n"
            f"Progression: {player_data.get('progressiveCarries')} progressive carries, {player_data.get('progressivePassesReceived')} progressive passes received\n"
            f"Defensive: {player_data.get('tacklesWonPercentage')}% tackle success, {player_data.get('aerialDuelsWonPercentage')}% aerial duels won\n\n"
            f"Based on these statistics, provide:\n"
            f"1. A technical evaluation of the player's strengths and weaknesses\n"
            f"2. Their primary playing style and tactical role\n"
            f"3. Areas for development considering their age and position\n"
            f"4. Comparison to positional benchmarks\n"
            f"5. Projection of potential and ideal tactical deployment\n\n"
            f"Format the analysis as a structured report with clear sections and data-supported insights."
        )

    def get_scouting_report(self, player_data):
        prompt = self.generate_prompt(player_data)

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert soccer analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1500,
        )

        generated_report = response.choices[0].message.content

        return generated_report


report_service = ReportService()
