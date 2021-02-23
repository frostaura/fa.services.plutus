using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.Configuration;
using System;
using System.IO;

namespace FrostAura.Services.Plutus.Data.Factories.DesignTime
{
  /// <summary>
  /// DB context factory for running migrations in design time.
  /// This allows for running migrations in the .Data project independently.
  /// </summary>
  public class PlutusDbContextDesignTimeFactory : IDesignTimeDbContextFactory<PlutusDbContext>
  {
    /// <summary>
    /// Factory method for producing the design time db context
    /// </summary>
    /// <param name="args"></param>
    /// <returns>Database context.</returns>
    public PlutusDbContext CreateDbContext(string[] args)
    {
      var configuration = new ConfigurationBuilder()
          .SetBasePath(Directory.GetCurrentDirectory())
          .AddJsonFile("appsettings.Migrations.json")
          .Build();
      var builder = new DbContextOptionsBuilder<PlutusDbContext>();
      var connectionString = configuration
          .GetConnectionString("PlutusDbConnection");

      builder.UseSqlServer(connectionString);

      Console.WriteLine($"Used connection string for configuration db: {connectionString}");

      return new PlutusDbContext(builder.Options);
    }
  }
}
