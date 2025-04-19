using System.ComponentModel.DataAnnotations;

namespace VideoClub.Models
{
	public class LoginModel
	{
		[Required, StringLength(50)]
		public string Username { get; set; }= string.Empty;

		[Required]
		public string Password { get; set; }= string.Empty;
	}
}
