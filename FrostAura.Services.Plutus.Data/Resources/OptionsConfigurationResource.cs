using FrostAura.Services.Plutus.Data.Interfaces;

namespace FrostAura.Services.Plutus.Data.Resources
{
  /// <summary>
  /// Configuration resource that uses options in the back-end.
  /// </summary>
  public class OptionsConfigurationResource : IConfigurationResource
  {
    /// <summary>
    /// Constructor to provide dependencies.
    /// </summary>
    /// <param name="options">Applications config MQTT configuration.</param>
    /*public OptionsConfigurationResource(IOptions<List<MqttAttributeProviderConfig>> options)
    {
        _mqttProvidersConfiguration = options
            .ThrowIfNull(nameof(options))
            .Value
            .ThrowIfNull(nameof(options.Value))
            .First();
    }*/

    /// <summary>
    /// Get the MQTT provider configuration.
    /// </summary>
    /// <returns>MQTT provider configuration.</returns>
    /*public MqttAttributeProviderConfig GetMqttAttributeProviders()
    {
        return _mqttProvidersConfiguration;
    }*/
  }
}
