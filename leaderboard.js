<!DOCTYPE html>
<html>
<head>
    <title>Ocean Heatwave Detection Challenge - Leaderboard</title>
    <link rel="stylesheet" href="leaderboard.css">
    <meta http-equiv="refresh" content="60">
</head>
<body>
    <div class="container">
        <h1>🌊 Ocean Heatwave Detection Challenge</h1>
        <h2>🏆 Live Leaderboard</h2>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Top Perturbed F1</h3>
                <div id="topF1">--</div>
            </div>
            <div class="stat-card">
                <h3>Most Robust Team</h3>
                <div id="mostRobust">--</div>
            </div>
            <div class="stat-card">
                <h3>Total Submissions</h3>
                <div id="totalSubmissions">--</div>
            </div>
        </div>
        
        <table id="leaderboard">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Team</th>
                    <th>Ideal F1</th>
                    <th>Perturbed F1 ⭐</th>
                    <th>Robustness Gap</th>
                    <th>Submission Date</th>
                </tr>
            </thead>
            <tbody id="leaderboard-body">
                <tr><td colspan="6">Loading...</td></tr>
            </tbody>
        </table>
        
        <div class="info">
            <h3>📊 Ranking Criteria:</h3>
            <ol>
                <li><strong>Primary:</strong> Highest Perturbed F1 Score</li>
                <li><strong>Secondary:</strong> Lowest Robustness Gap</li>
                <li><strong>Tertiary:</strong> Most recent submission</li>
            </ol>
            <p>🔄 Leaderboard updates automatically every minute</p>
            <p>🔒 All submissions are encrypted and evaluated blindly</p>
        </div>
    </div>
    
    <script src="leaderboard.js"></script>
</body>
</html>
