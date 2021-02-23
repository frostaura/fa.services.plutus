using FrostAura.Services.Plutus.Data.Interfaces;
using FrostAura.Services.Plutus.Data.Resources;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using System.Reflection;

namespace FrostAura.Services.Plutus.Data.Extensions
{
  /// <summary>
  /// Extensions for IServiceCollection.
  /// </summary>
  public static class ServiceCollectionExtensions
  {
    /// <summary>
    /// Add all required application resource services and config to the DI container.
    /// </summary>
    /// <param name="services">Application services collection.</param>
    /// <param name="config">Configuration for the application.</param>
    /// <returns>Application services collection.</returns>
    public static IServiceCollection AddFrostAuraResources(this IServiceCollection services, IConfiguration config)
    {
      return services
          .AddConfig(config)
          .AddServices();
    }

    /// <summary>
    /// Add all required application resources configuration to the DI container.
    /// </summary>
    /// <param name="services">Application services collection.</param>
    /// <returns>Application services collection.</returns>
    private static IServiceCollection AddConfig(this IServiceCollection services, IConfiguration config)
    {
      var plutusConnectionString = config.GetConnectionString("PlutusDbConnection");
      var migrationsAssembly = typeof(PlutusDbContext).GetTypeInfo().Assembly.GetName().Name;

      return services
          .AddDbContext<PlutusDbContext>(config =>
          {
            config
                      .UseSqlServer(plutusConnectionString)
                      .EnableSensitiveDataLogging();
          })
          .AddOptions();
    }

    /// <summary>
    /// Add all required application resource services to the DI container.
    /// </summary>
    /// <param name="services">Application services collection.</param>
    /// <returns>Application services collection.</returns>
    private static IServiceCollection AddServices(this IServiceCollection services)
    {
      return services
        .AddSingleton<IConfigurationResource, OptionsConfigurationResource>();
    }
  }
}
