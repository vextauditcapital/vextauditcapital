export const config = {
  matcher: ['/chairman-dashboard', '/chairman-dashboard.html'],
};

export default function middleware(request) {
  const authorizationHeader = request.headers.get('authorization');

  if (authorizationHeader) {
    const basicAuth = authorizationHeader.split(' ')[1];
    const [user, password] = atob(basicAuth).split(':');

    if (user === 'vextceo' && password === 'vac_admin_secure_778899') {
      return new Response(null, {
        headers: { 'x-middleware-next': '1' }
      });
    }
  }

  return new Response('Auth required', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Secure Area"',
    },
  });
}
