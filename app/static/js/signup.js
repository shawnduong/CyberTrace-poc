$("#signup").click(function()
{
	rtypewriter($("#authentication"), 50);
	rtypewriter($("#signup"), 15);
	rtypewriter($("#login-submit"), 75);

	/* Switch from authentication to registration. */
	if ($("#login-type").attr("value") == "login")
	{
		$("#login-type").attr("value", "signup");
		typewriter_d($("#authentication"), "Registration", 50, 800);
		typewriter_d($("#signup"), "Already have an account? Log in.", 15, 800);
		typewriter_d($("#login-submit"), "Sign Up", 60, 800);

		if ($("#login-failed"))
		{
			rtypewriter($("#login-failed"), 10);
		}
	}
	/* Switch from registration to authentication. */
	else
	{
		$("#login-type").attr("value", "login");
		typewriter_d($("#authentication"), "Authentication", 50, 800);
		typewriter_d($("#signup"), "Don't have an account? Sign up for one.", 15, 800);
		typewriter_d($("#login-submit"), "Log In", 60, 800);
	}
});
