
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils.timezone import now
import datetime


import json

VOTES_FILE = "votes.txt"

from django.shortcuts import render, redirect
from django.utils.timezone import now
import json

from django.shortcuts import render, redirect
from django.utils.timezone import now
import json
from datetime import datetime

VOTES_FILE = "votes.txt"

# Load votes from file
def load_votes():
    try:
        with open(VOTES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Mammootty": 0, "Mohanlal": 0, "Dulquar": 0}

# Save votes to file
def save_votes(votes):
    with open(VOTES_FILE, "w") as file:
        json.dump(votes, file)

# Voting function using session-based tracking
def vote(request):
    votes = load_votes()

    # Check if the user has already voted
    last_voted_time_str = request.session.get("last_voted_time")

    if last_voted_time_str:
        try:
            # Convert stored string time back to a datetime object
            last_voted_time = datetime.fromisoformat(last_voted_time_str)
            time_elapsed = (now() - last_voted_time).total_seconds()

            if time_elapsed < 3600:  # 1 hour = 3600 seconds
                return render(request, "vote.html", {"error": "You can vote again after 1 hour!"})
        except ValueError:
            pass  # Ignore if stored format is incorrect

    if request.method == "POST":
        candidate = request.POST.get("candidate")
        if candidate in votes:
            votes[candidate] += 1
            save_votes(votes)

            # Store the current time as an ISO 8601 string in session
            request.session["last_voted_time"] = now().isoformat()
            request.session.modified = True  # Ensure session is saved

        return redirect("vote_summary")

    return render(request, "vote.html")




def vote_summary(request):
    votes = load_votes()
    total_votes = sum(votes.values())

    print(votes)  # Debugging: Check if votes_count has data

    return render(request, "vote_summary.html", {
        "votes_count": votes,  # Pass dictionary directly
        "total_votes": total_votes
    })

