# EC500 HW4: FFMPEG
Jacob Davis

## Main exercise 
Using the twitter feed, construct a daily video summarizing a twitter handle day.
* Convert text into an image in a frame
* Do a sequence of all texts and images in chronological order.
* Display each video frame for 3 seconds

## Suggestions
* Establish a processing criteria:
  * How many API calls you can handle simultaneously and why?
  * For example, run different API calls at the same time?
  * Split the processing of an API into multiple threads?
* Recommendation for working on the homework:  
  * Step 1:
    * Develop a queue system that can exercise your requirements with stub functions.
  * Step 2: 
    * Develop the twitter functionality with an API
  * Step 3:
    * Integrate them
* Include tracking interface to show how many processes are going on and success of each