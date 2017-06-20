/**action types**/
export const LOGIN = 'LOGIN'

/**other constants**/
export const Preference ={	
	LIKE: 'LIKE',
	DISLIKE: 'DISLIKE'
}


/**login action creator**/
function attemptLogin(loggedIn, name) {
	return {
		type: LOGIN, 
		loggedIn,
		name
	}
}