using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;

namespace FrostAura.Services.Plutus.Api
{
  /// <summary>
  /// Program shell.
  /// </summary>
  public class Program
  {
    /// <summary>
    /// Entry function to the program.
    /// </summary>
    /// <param name="args">Command arguments passed.</param>
    public static void Main(string[] args)
    {
      CreateHostBuilder(args)
          .Build()
          .Run();
    }

    /// <summary>
    /// Build up web host application.
    /// </summary>
    /// <param name="args">Command arguments passed.param>
    /// <returns>Build application.</returns>
    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureWebHostDefaults(webBuilder =>
            {
              webBuilder.UseStartup<Startup>();
            });
  }
}
