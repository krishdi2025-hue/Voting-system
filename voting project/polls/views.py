from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import Candidate, Vote
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    candidates = Candidate.objects.order_by('number')
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    vote_obj = Vote.objects.filter(session_key=session_key).order_by('-created_at').first()
    voted_candidate_id = vote_obj.candidate.id if vote_obj else None
    return render(request, 'polls/index.html', {
        'candidates': candidates,
        'voted_candidate_id': voted_candidate_id
    })

@require_POST
def cast_vote(request):
    candidate_id = request.POST.get('candidate_id')
    if not candidate_id:
        return JsonResponse({'success': False, 'message': 'No candidate provided.'}, status=400)
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # check authenticated user first
    if request.user.is_authenticated:
        if Vote.objects.filter(user=request.user).exists():
            prev = Vote.objects.filter(user=request.user).order_by('-created_at').first()
            return JsonResponse({'success': False, 'message': 'You have already voted.', 'voted_candidate_id': prev.candidate.id}, status=403)
    else:
        if Vote.objects.filter(session_key=session_key).exists():
            prev = Vote.objects.filter(session_key=session_key).order_by('-created_at').first()
            return JsonResponse({'success': False, 'message': 'You have already voted.', 'voted_candidate_id': prev.candidate.id}, status=403)

    Vote.objects.create(candidate=candidate, session_key=session_key, user=request.user if request.user.is_authenticated else None)
    return JsonResponse({'success': True, 'message': 'Vote recorded.', 'voted_candidate_id': candidate.id})
from django.http import JsonResponse
from django.db.models import Count
from .models import Candidate, Vote

def voting_status(request):
    """
    Returns JSON with vote counts for all candidates and the current session/user's voted candidate (if any).
    Uses 'num_votes' as annotation name to avoid conflict with any 'votes' field.
    """
    # aggregate counts; NOTE: annotation name is num_votes (not votes)
    qs = Candidate.objects.annotate(num_votes=Count('votes')).order_by('number')

    counts = []
    total_votes = 0
    for c in qs:
        total_votes += c.num_votes
        counts.append({
            'candidate_id': c.id,
            'name': c.name,
            'number': c.number,
            # send as 'votes' in JSON, but read from c.num_votes
            'votes': c.num_votes,
        })

    # ensure session exists
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    voted_candidate_id = None
    if request.user.is_authenticated:
        v = Vote.objects.filter(user=request.user).order_by('-created_at').first()
        if v:
            voted_candidate_id = v.candidate.id
    if not voted_candidate_id:
        v = Vote.objects.filter(session_key=session_key).order_by('-created_at').first()
        if v:
            voted_candidate_id = v.candidate.id

    return JsonResponse({
        'success': True,
        'counts': counts,
        'total_votes': total_votes,
        'voted_candidate_id': voted_candidate_id,
    })
