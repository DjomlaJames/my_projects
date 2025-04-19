using Microsoft.JSInterop;
using System.Threading.Tasks;

namespace VideoClub.Services
{
	public class SessionService
	{
		private readonly IJSRuntime _jsRuntime;

		public SessionService(IJSRuntime jsRuntime)
		{
			_jsRuntime = jsRuntime;
		}

		public async Task SetUser(string username)
		{
			await _jsRuntime.InvokeVoidAsync("sessionStorage.setItem", "loggedInUser", username);
		}

		public async Task<string> GetUser()
		{
			return await _jsRuntime.InvokeAsync<string>("sessionStorage.getItem", "loggedInUser");
		}

		public async Task Logout()
		{

			await _jsRuntime.InvokeVoidAsync("sessionStorage.removeItem", "loggedInUser");
			await _jsRuntime.InvokeVoidAsync("sessionStorage.removeItem", "userRole");
		}

		public async Task SetUser(string username, string role)
		{
			await _jsRuntime.InvokeVoidAsync("sessionStorage.setItem", "loggedInUser", username);
			await _jsRuntime.InvokeVoidAsync("sessionStorage.setItem", "userRole", role);
		}

		public async Task ClearSession()
		{
			await _jsRuntime.InvokeVoidAsync("sessionStorage.clear"); // Brišemo sve podatke iz sesije
		}


		public async Task<string> GetUserRole()
		{
			try
			{
				return await _jsRuntime.InvokeAsync<string>("sessionStorage.getItem", "userRole");
			}
			catch (InvalidOperationException)
			{
				return ""; // Ako Blazor još nije spreman, vraćamo prazan string
			}
		}


	}
}
