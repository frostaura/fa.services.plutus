using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace FrostAura.Services.Plutus.Core.Extensions
{
  /// <summary>
  /// Extensions for IServiceCollection.
  /// </summary>
  public static class ServiceCollectionExtensions
  {
    /// <summary>
    /// Add all required application engine and manager services and config to the DI container.
    /// </summary>
    /// <param name="services">Application services collection.</param>
    /// <param name="config">Configuration for the application.</param>
    /// <returns>Application services collection.</returns>
    public static IServiceCollection AddFrostAuraCore(this IServiceCollection services, IConfiguration config)
    {
      return services
          .AddConfig(config)
          .AddServices();
    }

    /// <summary>
    /// Add all required application engines configuration to the DI container.
    /// </summary>
    /// <param name="services">Application services collection.</param>
    /// <param name="config">Configuration for the application.</param>
    /// <returns>Application services collection.</returns>
    private static IServiceCollection AddConfig(this IServiceCollection services, IConfiguration config)
    {

      return services;
    }

    /// <summary>
    /// Add all required application engine services to the DI container.
    /// </summary>
    /// <param name="services">Application services collection.</param>
    /// <returns>Application services collection.</returns>
    private static IServiceCollection AddServices(this IServiceCollection services)
    {
      return services;
    }
  }
}
