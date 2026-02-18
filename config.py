import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

FILE_PROJECTS = "projects.ods"
FILE_CURRENCIES = "currencies.ods"

BROWSER_LIMIT = 5
AI_LIMIT = 2
DEFAULT_CURRENCY = "€"

ALL_PAGES = ["Index", "Bonuses", "How to register", "Payments", "Betting", "About us", "Affiliates", "Responsible Gambling", "Casino App", "T & C", "Privacy Policy", "Login"]
AI_TARGET_PAGES = ["T & C", "Affiliates", "Responsible Gambling", "Privacy Policy"]

TEXT_TEMPLATES = {
    "BONUS_H2_4": "<p>We're excited to have you play with us. Before we begin, please take a moment to review our bonus rules:</p><ul><li><strong>Only one bonus can be active at a time</strong>.</li><li>Time limit: There is no specific time limit for completing wagering.</li><li>Game contribution percentages:<ul><li>Slot machines contribute 100% towards wagering requirements.</li><li>Table games contribute 20% towards wagering requirements.</li></ul></li><li>Eligibility rules: This offer is only available to new players who have not made a deposit before. One bonus per household/IP address.</li></ul><p>Let's get started and have some fun!</p>",
    "BONUS_H2_5": "<p>Get ready to unlock the full potential of your bonuses! Here are some practical tips to help you make the most out of them:</p><ul><li><strong>Choose games with high contribution rates</strong>: Not all games contribute equally to your bonus wagering requirements. Opt for slots, table games, or video poker that have a higher contribution rate to speed up your progress.</li><li><strong>Manage your bankroll wisely</strong>: Set a budget and stick to it. Make sure you're playing within your means to avoid depleting your funds quickly. Use the 10% rule as a guideline: allocate only 10% of your bankroll for bonus wagering.</li><li><strong>Don't forget to read the terms</strong>: Bonus offers often come with specific rules, such as minimum bets, maximum payouts, or game restrictions. Take the time to understand these conditions before you start playing to avoid any surprises down the line.</li><li><strong>Use loyalty rewards to extend play</strong>: Many online casinos offer loyalty programs that reward players for their continued patronage. These rewards can include free spins, cashback, or exclusive bonuses – use them wisely to stretch your bankroll and enjoy more gaming time.</li><li><strong>Track your wagering progress</strong>: Keep an eye on your bonus progress by monitoring your remaining wagering requirements. Some casinos provide a \"bonus meter\" or offer updates via email – take advantage of these tools to stay informed and adjust your strategy accordingly.</li></ul><p>Remember, bonuses are meant to enhance your gaming experience, not deplete your funds. By following these tips, you'll be well on your way to making the most out of your rewards and enjoying more time playing your favorite games!</p>",
    "CASINO_APP_H2_2": "<p><strong>For Android Devices:</strong></p><ol><li>Visit the [Casino Name]&nbsp;website on your device's web browser.</li><li>Tap download the app.</li><li>Select \"Download APK\" and follow the prompts to save the file.</li><li>Locate the downloaded APK file in your device's downloads folder.</li><li><strong>Tap the APK file to install</strong>; allow system permissions to enable installation.</li></ol><p><strong>For iOS Devices:</strong></p><ul><li>Open the App Store on your iOS device.</li><li>Search for \"[Casino Name]\" in the search bar.</li><li>Select the [Casino Name]&nbsp;app from the results and <strong>tap \"Get\"</strong> to download.</li><li>If prompted, enter your Apple ID password or use Face/Touch ID authentication.</li><li>Once installed, tap \"Open\" to access the [Casino Name]&nbsp;app.</li></ul>"
}