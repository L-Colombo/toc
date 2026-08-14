{
  description = "A CLI utility to add table of contents to PDFs";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell {
        strictDeps = true;

        nativeBuildInputs = with pkgs; [
          python313
          uv
        ];

        buildInputs = with pkgs; [
          libclang
        ];

        shellHook = ''
          export PS1="(dev) $PS1"
        '';

        LIBCLANG_PATH = with pkgs; "${libclang.lib}/lib";
      };
    };
}
