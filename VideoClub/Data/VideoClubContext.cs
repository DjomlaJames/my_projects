using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using VideoClub.Models;

namespace VideoClub.Data
{
    public class VideoClubContext : DbContext
    {
        public VideoClubContext (DbContextOptions<VideoClubContext> options)
            : base(options)
        {
        }

        public DbSet<VideoClub.Models.User> Users { get; set; } = default!;
		public DbSet<Movie> Movies { get; set; } = default!;
		public DbSet<Order> Orders { get; set; } = default!;


		protected override void OnModelCreating(ModelBuilder modelBuilder)
		{
			base.OnModelCreating(modelBuilder);
			modelBuilder.Entity<User>().ToTable("Users"); // Ovim sprečavamo ponovno kreiranje tabele



			// Postavi jedinstveni email
			modelBuilder.Entity<User>()
				.HasIndex(u => u.Email)
				.IsUnique();

			// Postavi podrazumevanu vrednost za Role
			modelBuilder.Entity<User>()
				.Property(u => u.Role)
				.HasDefaultValue("user");

			modelBuilder.Entity<User>()
				.HasIndex(u => u.Username)
				.IsUnique();

			modelBuilder.Entity<Movie>()
				.Property(m => m.Genre)
				.HasConversion<string>(); 

			modelBuilder.Entity<Movie>()
				.Property(m => m.Rating)
				.HasConversion<string>();
			modelBuilder.Entity<Order>()
				.HasOne(o => o.User)
				.WithMany()
				.HasForeignKey(o => o.UserId)
				.OnDelete(DeleteBehavior.Cascade);

			modelBuilder.Entity<Order>()
				.HasOne(o => o.Movie)
				.WithMany()
				.HasForeignKey(o => o.MovieId)
				.OnDelete(DeleteBehavior.Cascade);

		}
	}
}
