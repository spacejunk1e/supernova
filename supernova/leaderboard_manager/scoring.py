"""
Scoring Module
---------------

This module provides functions to calculate scores for users based on their activity.
It factors in post frequencies, reactions, and other metrics to assign a user score.

Functions:
- post_within_timeframe: Helper function to check if a post falls within a given timeframe.
- calculate_base_post_points: Calculates points based on the number of posts.
- calculate_reaction_points: Calculates points based on the reactions received on posts.
- calculate_diversity_multiplier: Determines a multiplier based on diversity of post content types.
- calculate_frequency_decay: Adjusts score based on post frequency.
- calculate_unique_reactor_bonus: Awards bonus points for unique reactors to a user's posts.
- calculate_curator_bonus: Awards bonus points for posts marked by curators.
"""

from datetime import datetime, timedelta
from .config import (
    BASE_POST_POINT,
    REACTION_POINTS,
    DIVERSITY_MULTIPLIER,
    FREQUENCY_DECAY_THRESHOLD,
    FREQUENCY_DECAY_RATE,
    UNIQUE_REACTOR_BONUS,
    CURATOR_BONUS)


def post_within_timeframe(post, timeframe):
    """
    Determine if a post falls within a specified timeframe.

    Parameters
    ----------
    post : Post
        The post for which the check is being made.
    timeframe : str
        The desired timeframe to check against. Options are 'daily', 'weekly', or 'monthly'.

    Returns
    -------
    bool
        True if the post is within the specified timeframe, otherwise False.
    """

    now = datetime.now()
    if timeframe == 'daily':
        return post.timestamp > now - timedelta(days=1)
    elif timeframe == 'weekly':
        return post.timestamp > now - timedelta(weeks=1)
    elif timeframe == 'monthly':
        return post.timestamp > now - timedelta(days=30)
    return False


def calculate_base_post_points(user):
    """
    Calculate the total points based on the number of posts made by the user.

    Parameters
    ----------
    user : User
        The user for whom the points are being calculated.

    Returns
    -------
    float
        The total points based on the number of posts.
    """

    return len(user.posts) * BASE_POST_POINT


def calculate_reaction_points(user):
    """
    Calculate the total points based on reactions received on the user's posts.

    Parameters
    ----------
    user : User
        The user for whom the points are being calculated.

    Returns
    -------
    float
        The total points based on reactions.
    """

    total = 0
    for post in user.posts:
        for reaction in post.reactions:
            total += REACTION_POINTS.get(reaction.type, REACTION_POINTS['generic'])
    return total


def calculate_diversity_multiplier(user):
    """
    Calculate a multiplier based on the diversity of content types the user has posted.

    Parameters
    ----------
    user : User
        The user for whom the multiplier is being calculated.

    Returns
    -------
    float
        The diversity multiplier (either DIVERSITY_MULTIPLIER or 1).
    """

    unique_content_types = set([post.content_type for post in user.posts])
    return DIVERSITY_MULTIPLIER if len(unique_content_types) > 1 else 1


def calculate_frequency_decay(user, timeframe='daily'):
    """
    Calculate score decay if the user has posted too frequently within a given timeframe.

    Parameters
    ----------
    user : User
        The user for whom the decay is being calculated.
    timeframe : str, optional
        The timeframe for considering post frequency, by default 'daily'.

    Returns
    -------
    float
        The score decay based on post frequency.
    """

    recent_posts = [post for post in user.posts if post_within_timeframe(post, timeframe)]
    if len(recent_posts) > FREQUENCY_DECAY_THRESHOLD:
        excess = len(recent_posts) - FREQUENCY_DECAY_THRESHOLD
        return excess * BASE_POST_POINT * FREQUENCY_DECAY_RATE
    return 0


def calculate_unique_reactor_bonus(user):
    """
    Calculate bonus points based on unique reactors to the user's posts.

    Parameters
    ----------
    user : User
        The user for whom the bonus is being calculated.

    Returns
    -------
    float
        The bonus points based on unique reactors.
    """

    unique_reactors = set()
    for post in user.posts:
        for reaction in post.reactions:
            unique_reactors.add(reaction.reactor)
    return len(unique_reactors) * UNIQUE_REACTOR_BONUS


def calculate_curator_bonus(user):
    """
    Calculate bonus points for posts marked as 'curator's pick'.

    Parameters
    ----------
    user : User
        The user for whom the bonus is being calculated.

    Returns
    -------
    float
        The bonus points for curator-picked posts.
    """

    curator_reactions = sum(1 for post in user.posts for r in post.reactions if r.type == 'curator_pick')
    return curator_reactions * CURATOR_BONUS
