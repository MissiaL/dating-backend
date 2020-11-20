from api import views

paths = {
    'users': [
        ('/users/', 'GET', views.get_users),
        ('/users/', 'POST', views.create_user),
        ('/users/{user_id}/', 'PATCH', views.update_user),
        ('/users/{user_id}/', 'DELETE', views.delete_user),
    ],
    'costs': [
        ('/costs/', 'GET', views.get_costs),
        ('/costs/', 'POST', views.create_cost),
        ('/costs/{cost_id}/', 'PATCH', views.update_cost),
        ('/costs/{cost_id}/', 'DELETE', views.delete_cost),
    ],
    'photo': [
        ('/photos/', 'GET', views.get_photos),
        ('/photos/', 'POST', views.create_photo),
        ('/photos/{photo_id}/', 'PATCH', views.update_photo),
        ('/photos/{photo_id}/', 'DELETE', views.delete_photo),
    ],
    'action': [
        ('/actions/', 'GET', views.get_actions),
        ('/actions/', 'POST', views.create_action),
        ('/actions/{action_id}/', 'PATCH', views.update_action),
        ('/actions/{action_id}/', 'DELETE', views.delete_action),
    ],
    'message': [
        ('/messages/', 'GET', views.get_messages),
        ('/messages/', 'POST', views.create_message),
        ('/messages/{message_id}/', 'PATCH', views.update_message),
        ('/messages/{message_id}/', 'DELETE', views.delete_message),
    ],
}

