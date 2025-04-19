using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace VideoClub.Models;

public class Movie
{
	public int Id { get; set; }

	[Required, StringLength(100)]
	public string? Title { get; set; }

	[Required, Range(1900, 2100)]
	public int DateRelease { get; set; }

	[Required]
	[RegularExpression(@"^(Action|Adventure|Animation|Biography|Comedy|Crime|Documentary|Drama|Family|Fantasy|History|Horror|Musical|Mystery|Romance|Sci-Fi|Sport|Thriller|War|Western)$")]
	public string Genre { get; set; } = string.Empty;

	[Required]
	[RegularExpression(@"^(G|PG|PG-13|R|NC-17)$")]
	public string? Rating { get; set; }

	[Required, Range(0, 100)]
	public int Stocks { get; set; }

	[Required]
	[DataType(DataType.Currency)]
	[Column(TypeName = "decimal(18, 2)")]
	public decimal Price { get; set; }
}

