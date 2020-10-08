# Phase 2 Final Project



Student name: Kourosh Alizadeh  
Student pace: full time  
Scheduled project review date/time: 10/12/2020, 3pm EST  
Instructor name: Rafael Carrasco  
Blog post URL: TBD  

## An Examination of the Housing Habits of the Human Aliens

To my dear and esteemed colleagues of the Alien Species Research Comission:

Thanks to our brave agents in the field, we have recently acquired some data on patterns regarding the artifical habitats humans have created for themselves in a place called King's County. 

In this report, we use this data to examine what features humans value in a dwelling. In particular, we look at the following questions:

1. Do humans prefer to live near water or to live more inland where it is safer?
2. Do humans like to have a lot of empty land around them?
3. Do humans like to live high above the ground?
4. Do humans enjoy living deep below the ground?
5. Do humans use their eyes for pleasure or only survival?

Finally, we build a model using multlinear regression to estimate how a human might value a house based on its features. 

To begin with, let's look at the results for each question:

### 1. Do humans prefer to live near water?

![title](images/waterfront.png)

Yes, they do. Houses built near the water predominantly among the most expensive.



### 2. Do humans like to have empty land around them?

![title](images/surroundings.png)

There does not seem to be any connection between the amount of surrounding space a house has and a human's willingness to expend financial tokens for its purchase.

### 3. Do humans value living high above the ground?

![title](images/tallness.png)

Yes, they do. There are more tall homes among the upper quartile than there are among lower quartiles. 

### 4. Do humans enjoy living deep beneath the ground?

![title](images/basements.png)

Yes. Basements, like access to water and high floors, also seemed to be more common among more expensive homes. 

### 5. Do humans use their eyes for pleasure?

![title](images/view.png)

Yes. While some had argued previously that the human eye was simply a way of sensing radiation for survival purposes, humans do seem to value experiencing certain patterns of radiation more than others, regardless of survivability. They are willing to spend more on homes that enable them to experience these preferred patterns more often.

## Our Regression Model

We used most of these features, as well as the log sqftage of the living space in each artifical habitat, to build a multiple regression model.

![title](images/regression.png)

The strongest coefficient was the one associated with the log of living space. As that number goes up, so too does the log of price. The coefficients of the basement and the high floors features were negative. This is a little surprising, since we know there is a positive correlation between these features and the price of homes. But their negative contribution here must be a sign of them balancing out some other feature, likely the living space one. Last, the view features did not contribute too much to our model, but they did do something, and their p-values indicate that they were reasonably significant.

## Recommendations


