using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace VideoClub.Migrations
{
	/// <inheritdoc />
	public partial class AddMoviesTable : Migration
	{
		/// <inheritdoc />
		protected override void Up(MigrationBuilder migrationBuilder)
		{
			// Kreira samo Movies tabelu, bez Users
			migrationBuilder.CreateTable(
				name: "Movies",
				columns: table => new
				{
					Id = table.Column<int>(type: "int", nullable: false)
						.Annotation("SqlServer:Identity", "1, 1"),
					Title = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
					DateRelease = table.Column<int>(type: "int", nullable: false),
					Genre = table.Column<string>(type: "nvarchar(max)", nullable: false),
					Rating = table.Column<string>(type: "nvarchar(max)", nullable: false),
					Stocks = table.Column<int>(type: "int", nullable: false),
					Price = table.Column<decimal>(type: "decimal(18,2)", nullable: false)
				},
				constraints: table =>
				{
					table.PrimaryKey("PK_Movies", x => x.Id);
				});
		}

		/// <inheritdoc />
		protected override void Down(MigrationBuilder migrationBuilder)
		{
			// Briše samo Movies tabelu, bez Users
			migrationBuilder.DropTable(
				name: "Movies");
		}
	}
}

