using VideoClub.Components;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using VideoClub.Data;
using Microsoft.AspNetCore.Components.Server.ProtectedBrowserStorage;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContextFactory<VideoClubContext>(options =>
{
    options.UseSqlServer(builder.Configuration.GetConnectionString("VideoClubContext") ?? throw new InvalidOperationException("Connection string 'VideoClubContext' not found."), options => options.EnableRetryOnFailure());
},ServiceLifetime.Transient);

builder.Services.AddQuickGridEntityFrameworkAdapter();


builder.Services.AddScoped<ProtectedLocalStorage>(); 
builder.Services.AddScoped<ProtectedSessionStorage>();
builder.Services.AddTransient<VideoClub.Services.SessionService>();

builder.Services.AddDatabaseDeveloperPageExceptionFilter();

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();



var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
    app.UseMigrationsEndPoint();
}

app.UseHttpsRedirection();


app.UseAntiforgery();

app.MapStaticAssets();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();
