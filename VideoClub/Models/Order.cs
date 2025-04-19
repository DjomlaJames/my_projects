using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace VideoClub.Models
{
	public class Order
	{
		[Key]
		public int Id { get; set; }

		[Required]
		public int UserId { get; set; }

		[Required]
		public int MovieId { get; set; }

		[Required]
		[Column(TypeName = "decimal(18, 2)")]
		public decimal Price { get; set; }

		[Required]
		public DateTime OrderDate { get; set; } = DateTime.Now;

		// Relacije sa tabelama Users i Movies
		[ForeignKey("UserId")]
		public User? User { get; set; }

		[ForeignKey("MovieId")]
		public Movie? Movie { get; set; }
	}
}
