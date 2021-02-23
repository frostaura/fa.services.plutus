# Specify base image.
FROM mcr.microsoft.com/dotnet/core/sdk:3.1 AS build-env
WORKDIR /app

# Copy everything and restore / publish the solution.
COPY . ./
RUN dotnet build ./FrostAura.Services.Plutus.Api/FrostAura.Services.Plutus.Api.csproj
RUN dotnet test ./FrostAura.Services.Plutus.Core.Tests/FrostAura.Services.Plutus.Core.Tests.csproj
RUN dotnet test ./FrostAura.Services.Plutus.Data.Tests/FrostAura.Services.Plutus.Data.Tests.csproj
RUN dotnet publish ./FrostAura.Services.Plutus.Api/FrostAura.Services.Plutus.Api.csproj -c Release -o /app/out

# Build runtime image off the correct base.
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "FrostAura.Services.Plutus.Api.dll"]
EXPOSE 80