
import jwt

# Verify the token. Return the user and attachment_id on success
# and None on failure.
def verify_token(request, token):
    secret = request.env["ir.config_parameter"].sudo().get_param('cool_jwt_secret')
    if secret is None:
        return {
            'error': 'JWT is not configured.'
        }

    jwt_payload = None
    try:
        jwt_payload = jwt.decode(token, secret, algorithms=['HS256'])
    except Exception as e:
        return {
            'error': e
        }

    if jwt_payload is None:
        return {
            'error': 'JWT token failed to decode.'
        }

    attachment_id = jwt_payload['fid']
    if attachment_id is None:
        return {
            'error': 'Missing file.'
        }

    user_id = jwt_payload['uid']
    user = request.env["res.users"].sudo().browse(user_id).exists().ensure_one()
    if user is None:
        return {
            'error': 'User not found.'
        }

    res = {
        'user': user,
        'user_id': user_id,
        'attachment_id': attachment_id,
    }
    return res
