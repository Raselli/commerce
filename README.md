# CS50 Web Project 2: "commerce"
This project is an assignment from the course: [CS50 Web Programming with Python and Javascript](https://cs50.harvard.edu/web/2020/).

## Assignment
Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.” Assignment details [here](https://cs50.harvard.edu/web/2020/projects/2/commerce/).

## Project Description
The webpage is divided into several sections:
* Active Listings: This is the index of the page, containing all active auctions. Logged in users can bid on listed items.
* Add Listing: Redirects to the create-listing subpage, where a user may create a new auction. Certain fields are required (Listing name, starting bid, description). The user has the option to add an image to the auction and select a listing-category. Login is required.
* Categories: Under this section, a user will find the listings divided by category. Only admins have permission to create new categories. A category can be added to a listing optionally when creating it. 
* Watchlist: Each user has its own watchlist. Items can be added to and removed from the watchlist. Loggin is required.\
When clicking on a listing, the user is redirected to the listed item’s subpage where all information about the listing and the listings image are rendered. 
* The listed item page contains a button to add the listing to one’s watchlist.
* If the user has created the auction, the user has the option to close the auction which will also inform the winner.
* Each listing has a comment section where logged in users may leave a comment.\
Admins are allowed to edit all database entries including users, listings, watchlist, comments, bids and categories.

## Technical Description
Django handles all server request and database entries (in Python). 
The database consists of several related models (models.py).

## Project Demo
Click [here](https://youtu.be/WKVmT6mSK3Q) to watch a demonstration of this project on YouTube.

## Distribution Code 
[Distribution Code](https://cdn.cs50.net/web/2020/spring/projects/2/commerce.zip). 
All further requirements and terminal commands to run this project are found on the [Project Assignment Page](https://cs50.harvard.edu/web/2020/projects/2/commerce/)

