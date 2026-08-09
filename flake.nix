{
  # at the moment, used for testing the hook scripts in `plugins/extra/hooks/`
  description = "python toolchain for loam";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            git
            python3
            uv
            ruff
            pre-commit
          ];

          env = {
            # make uv use the Nix-provided Python instead of downloading its own.
            UV_PYTHON_DOWNLOADS = "never";
            UV_PYTHON = "${pkgs.python3}/bin/python3";
          };
        };
      });
}
