#!/usr/bin/env node

/**
 * CLI installer for Niels With Them Skills.
 * Installs skills, agent personas, and shared references into a project's agent directory (default: .agents).
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');

// ANSI Color Helpers
const colors = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  green: '\x1b[32m',
  cyan: '\x1b[36m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
};

function parseArgs(args) {
  const options = {
    help: false,
    list: false,
    all: false,
    skills: [],
    includeAgents: false,
    includeReferences: false,
    target: '.agents',
    symlink: false,
    force: false,
    dryRun: false,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else if (arg === '--list' || arg === '-l') {
      options.list = true;
    } else if (arg === '--all') {
      options.all = true;
    } else if (arg === '--agents' || arg === '-a') {
      options.includeAgents = true;
    } else if (arg === '--references' || arg === '-r') {
      options.includeReferences = true;
    } else if (arg === '--symlink') {
      options.symlink = true;
    } else if (arg === '--force' || arg === '-f') {
      options.force = true;
    } else if (arg === '--dry-run') {
      options.dryRun = true;
    } else if (arg === '--target' || arg === '-t') {
      options.target = args[++i];
    } else if (arg === '--skill' || arg === '-s') {
      const val = args[++i];
      if (val) {
        options.skills.push(...val.split(',').map((s) => s.trim()));
      }
    } else if (!arg.startsWith('-')) {
      // Positional argument: treat as skill name or 'all'
      if (arg === 'all') {
        options.all = true;
      } else {
        options.skills.push(arg);
      }
    }
  }

  return options;
}

function printHelp() {
  console.log(`
${colors.bold}Niels With Them Skills — Agent Package Installer${colors.reset}

${colors.dim}Install production-grade skills, agent personas, and references into your AI agent environment.${colors.reset}

${colors.bold}USAGE:${colors.reset}
  npx niels-with-them-skills [options] [skill-name...]
  npx github:NielsElmgaard/niels-with-them-skills [options] [skill-name...]

${colors.bold}OPTIONS:${colors.reset}
  -s, --skill <name>     Install specific skill(s) (comma-separated or repeatable)
  --all                  Install all available skills, agent personas, and references
  -a, --agents           Install agent personas into <target>/agents/
  -r, --references       Install shared reference checklists into <target>/references/
  -t, --target <dir>     Target destination directory (default: ${colors.cyan}.agents${colors.reset})
  --symlink              Create symlinks instead of copying files
  -f, --force            Overwrite existing files without prompting
  --dry-run              Preview installation actions without writing files
  -l, --list             List all available skills and agent personas
  -h, --help             Show this help message

${colors.bold}EXAMPLES:${colors.reset}
  # List all available skills
  npx niels-with-them-skills --list

  # Install a specific skill (e.g. skill-creator) into .agents/skills/
  npx niels-with-them-skills --skill skill-creator

  # Install all skills and agent personas
  npx niels-with-them-skills --all

  # Install into a custom agent directory (e.g. .claude or .cursor)
  npx niels-with-them-skills --skill skill-creator --target .claude
`);
}

function getAvailableSkills() {
  const skillsDir = path.join(REPO_ROOT, 'skills');
  if (!fs.existsSync(skillsDir)) return [];

  return fs.readdirSync(skillsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => {
      const skillName = entry.name;
      const skillMd = path.join(skillsDir, skillName, 'SKILL.md');
      let description = '';

      if (fs.existsSync(skillMd)) {
        const content = fs.readFileSync(skillMd, 'utf8');
        const match = content.match(/^---\n([\s\S]*?)\n---/);
        if (match) {
          const descMatch = match[1].match(/^description:\s*(.*)$/m);
          if (descMatch) {
            description = descMatch[1].trim().replace(/^['">| -]+/, '');
          }
        }
      }

      return { name: skillName, description };
    });
}

function getAvailableAgents() {
  const agentsDir = path.join(REPO_ROOT, 'agents');
  if (!fs.existsSync(agentsDir)) return [];

  return fs.readdirSync(agentsDir, { withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith('.md'))
    .map((entry) => entry.name.replace(/\.md$/, ''));
}

function printList() {
  const skills = getAvailableSkills();
  const agents = getAvailableAgents();

  console.log(`\n${colors.bold}Available Skills in Niels With Them Skills:${colors.reset}\n`);
  if (skills.length === 0) {
    console.log(`  ${colors.dim}(None found)${colors.reset}`);
  } else {
    for (const skill of skills) {
      console.log(`  • ${colors.bold}${colors.green}${skill.name}${colors.reset}`);
      if (skill.description) {
        console.log(`    ${colors.dim}${skill.description}${colors.reset}`);
      }
    }
  }

  console.log(`\n${colors.bold}Available Agent Personas:${colors.reset}\n`);
  if (agents.length === 0) {
    console.log(`  ${colors.dim}(None configured yet in agents/)${colors.reset}`);
  } else {
    for (const agent of agents) {
      console.log(`  • ${colors.cyan}${agent}${colors.reset}`);
    }
  }

  console.log(`\n${colors.dim}To install: npx niels-with-them-skills --skill <name>${colors.reset}\n`);
}

function installDirectory(sourceDir, destDir, { symlink, force, dryRun, label }) {
  if (dryRun) {
    console.log(`  ${colors.yellow}[dry-run]${colors.reset} Would install ${label} -> ${destDir}`);
    return;
  }

  if (fs.existsSync(destDir)) {
    if (!force) {
      console.log(`  ${colors.yellow}Notice:${colors.reset} ${destDir} already exists. Use ${colors.bold}--force${colors.reset} to overwrite.`);
      return;
    }
    fs.rmSync(destDir, { recursive: true, force: true });
  }

  fs.mkdirSync(path.dirname(destDir), { recursive: true });

  if (symlink) {
    fs.symlinkSync(sourceDir, destDir, 'junction');
    console.log(`  ${colors.green}✓${colors.reset} Symlinked ${colors.bold}${label}${colors.reset} -> ${destDir}`);
  } else {
    fs.cpSync(sourceDir, destDir, { recursive: true });
    console.log(`  ${colors.green}✓${colors.reset} Installed ${colors.bold}${label}${colors.reset} -> ${destDir}`);
  }
}

function main() {
  const options = parseArgs(process.argv.slice(2));

  if (options.help) {
    printHelp();
    return;
  }

  if (options.list) {
    printList();
    return;
  }

  const availableSkills = getAvailableSkills();
  const availableSkillNames = availableSkills.map((s) => s.name);

  // If no action specified, show list and usage
  if (!options.all && options.skills.length === 0 && !options.includeAgents && !options.includeReferences) {
    printHelp();
    printList();
    return;
  }

  const cwd = process.cwd();
  const targetBase = path.resolve(cwd, options.target);

  console.log(`\n${colors.bold}Installing into:${colors.reset} ${colors.cyan}${targetBase}${colors.reset}\n`);

  // 1. Determine skills to install
  let skillsToInstall = [];
  if (options.all || options.skills.includes('all') || options.skills.includes('*')) {
    skillsToInstall = availableSkillNames;
  } else {
    for (const requested of options.skills) {
      if (availableSkillNames.includes(requested)) {
        skillsToInstall.push(requested);
      } else {
        console.error(`  ${colors.red}✗ Skill not found:${colors.reset} "${requested}"`);
        console.error(`    Run with ${colors.bold}--list${colors.reset} to see available skills.`);
      }
    }
  }

  // 2. Install Skills
  for (const skillName of skillsToInstall) {
    const src = path.join(REPO_ROOT, 'skills', skillName);
    const dest = path.join(targetBase, 'skills', skillName);
    installDirectory(src, dest, {
      symlink: options.symlink,
      force: options.force,
      dryRun: options.dryRun,
      label: `skill '${skillName}'`,
    });
  }

  // 3. Install Agents (if requested or --all)
  if (options.all || options.includeAgents) {
    const agentsSrc = path.join(REPO_ROOT, 'agents');
    if (fs.existsSync(agentsSrc)) {
      const files = fs.readdirSync(agentsSrc).filter((f) => f.endsWith('.md'));
      if (files.length > 0) {
        const dest = path.join(targetBase, 'agents');
        installDirectory(agentsSrc, dest, {
          symlink: options.symlink,
          force: options.force,
          dryRun: options.dryRun,
          label: 'agent personas',
        });
      }
    }
  }

  // 4. Install Shared References (if requested or if skills installed or --all)
  if (options.all || options.includeReferences || skillsToInstall.length > 0) {
    const refsSrc = path.join(REPO_ROOT, 'references');
    if (fs.existsSync(refsSrc)) {
      const dest = path.join(targetBase, 'references');
      installDirectory(refsSrc, dest, {
        symlink: options.symlink,
        force: options.force,
        dryRun: options.dryRun,
        label: 'shared references',
      });
    }
  }

  console.log(`\n${colors.bold}${colors.green}Done!${colors.reset} Your agent can now discover these capabilities in ${colors.cyan}${options.target}/${colors.reset}.\n`);
}

main();
