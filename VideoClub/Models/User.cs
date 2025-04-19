using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Security.Cryptography;
using System.Text;
namespace VideoClub.Models
{
	public class User
	{
		[Key]
		public int Id { get; set; }

		[Required, StringLength(50)]
		public string FirstName { get; set; } = string.Empty;

		[Required, StringLength(50)]
		public string LastName { get; set; } = string.Empty;

		[Required, StringLength(50)]
		public string Username { get; set; } = string.Empty;

		[Required, EmailAddress]
		public string Email { get; set; } = string.Empty;

		[Required]
		public string Password { get; set; } = string.Empty;

		[NotMapped] // Neće se čuvati u bazi, koristiće se samo za validaciju
		[Compare("Password", ErrorMessage = "Passwords do not match.")]
		public string ConfirmPassword { get; set; } = string.Empty;

		[Required]
		public string Role { get; set; } = "user";
	}
}
