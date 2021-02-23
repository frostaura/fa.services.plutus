using Microsoft.EntityFrameworkCore;

namespace FrostAura.Services.Plutus.Data
{
  /// <summary>
  /// Plutus database context.
  /// </summary>
  public class PlutusDbContext : DbContext
  {
    /// <summary>
    /// Mapped attribute values.
    /// </summary>
    //public virtual DbSet<DeviceAttribute> DeviceAttributes { get; set; }

    /// <summary>
    /// Construct and allow for passing options.
    /// </summary>
    /// <param name="options">Db creation options.</param>
    public PlutusDbContext(DbContextOptions<PlutusDbContext> options)
        : base(options)
    { }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
      /*modelBuilder
          .Entity<Device>()
          .HasIndex(d => d.Name)
          .IsUnique(true);*/

      base.OnModelCreating(modelBuilder);
    }
  }
}