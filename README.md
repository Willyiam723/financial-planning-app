<h3> Main mechanics of the application </h3>

- A python program that helps user to determine an appropriate asset allocation for their long-term financial planning
- The program will first prompt user for some general personal information including full name, gender and date of birth, as well as financial related questions consisting of 8 multiple choice questions
- The financial questions are pre-drafted and saved in text files under the same directory as the program
- The program simply reads and outputs those questions for user’s response
- The program then takes those responses to determine the user's financial metrics including investment objectives, investment time horizon, income requirements and risk tolerances via an algorithm

    <img src='https://github.com/Willyiam723/Willyiam723/blob/master/config/financial-planning-app.png' width = 50%>

<h3> Design decisions </h3>

- The algorithm is designed as a scoring system where each option user selected will accumulate points towards one specific level of user’s financial metrics
- The level that has the most score is determined as the level of that financial metrics for the user
    - For example, risk tolerance has five levels including “zero”, “low”, “medium”, “high” and “very high”
- Depends on the option user selected as a response, one level will accumulate one point at a time for each question
- The program takes the risk tolerance level that has the highest score as the user’s level of risk tolerance
- Based on the determined investment objectives, investment time horizon, income requirements and risk tolerances, the program places the user’s financial needs into a mandate with an asset allocation plan tailored for the user (i.e. % of public equity, % of public and private fixed income, % of private equity, % of real estate, % of cash, % of hedge funds as part of total asset allocation)