from django.http import JsonResponse
from .models import Bot, Match
from .utils import play_match
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return JsonResponse({'message': 'User registered successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_bot(request):
    """
    Handles bot file upload and triggers matches with all existing bots.
    """
    user = request.user
    bot_name = request.data.get('name')
    bot_file = request.FILES['file']

    # Save the new bot
    new_bot = Bot.objects.create(user=user, name=bot_name, file=bot_file, chips=10000)

    # Trigger matches with all existing bots
    existing_bots = Bot.objects.exclude(id=new_bot.id)  # Exclude the newly uploaded bot
    results = []
    for existing_bot in existing_bots:
        winner, chips_exchanged = play_match(new_bot.file.path, existing_bot.file.path, new_bot, existing_bot)
        results.append({
            'opponent': existing_bot.name,
            'winner': winner,
            'chips_exchanged': chips_exchanged
        })

    return JsonResponse({
        'message': 'Bot uploaded successfully and matches played.',
        'results': results,
    })


def run_match(request, bot1_id, bot2_id):
    bot1 = Bot.objects.get(id=bot1_id)
    bot2 = Bot.objects.get(id=bot2_id)

    winner, chips_exchanged = play_match(bot1.file.path, bot2.file.path, bot1, bot2)

    match = Match(bot1=bot1, bot2=bot2, result=winner, chips_exchanged=chips_exchanged)
    match.save()

    return JsonResponse({
        'message': 'Match played',
        'winner': winner,
        'chips_exchanged': chips_exchanged,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    bots = Bot.objects.all().order_by('-chips')
    data = [{'name': bot.name, 'chips': bot.chips, 'owner': bot.user.username} for bot in bots]
    return JsonResponse(data, safe=False)
